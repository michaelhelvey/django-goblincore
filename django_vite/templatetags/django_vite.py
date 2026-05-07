import json
from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from urllib.parse import urljoin

DEBUG = settings.DEBUG
config = getattr(settings, "DJANGO_VITE", {})

manifest_path = config.get("manifest_path")
dev_command = config.get("dev_command")
dev_server = config.get("dev_server", "http://localhost:5173")
prod_mode = config.get("prod_mode", not DEBUG)

if not manifest_path:
    raise ValueError(
        "DJANGO_VITE setting must include 'manifest_path' pointing to the Vite manifest.json file produced by `vite build`"
    )

if not dev_command:
    raise ValueError(
        "DJANGO_VITE setting must include 'dev_command' specifying the command to start the Vite dev server (e.g. 'pnpm exec vite')"
    )

if dev_server and dev_server.endswith("/"):
    dev_server = dev_server[:-1]


register = template.Library()

if prod_mode:
    # In production, we need to load the manifest once and cache it for performance
    with open(manifest_path) as f:
        manifest_data = json.load(f)


@register.simple_tag
def vite_hmr_client():
    if not prod_mode:
        return format_html(
            '<script type="module" src="{dev_server}/@vite/client"></script>', dev_server=dev_server
        )
    return ""


@register.simple_tag
def vite_react_refresh_runtime():
    if not prod_mode:
        return format_html(
            """
<script type="module">
  import RefreshRuntime from '{dev_server}/@react-refresh';
  RefreshRuntime.injectIntoGlobalHook(window);
  window.$RefreshReg$ = () => {{}};
  window.$RefreshSig$ = () => (type) => type;
  window.__vite_plugin_react_preamble_installed__ = true;
</script>
    """.strip(),
            dev_server=dev_server,
        )
    return ""


@register.simple_tag
def vite_asset(entry_point):
    if not prod_mode:
        if is_css_asset(entry_point):
            return format_html(
                '<link rel="stylesheet" href="{dev_server}/{entry_point}">',
                dev_server=dev_server,
                entry_point=entry_point,
            )

        return format_html(
            '<script type="module" crossorigin src="{dev_server}/{entry_point}"></script>',
            dev_server=dev_server,
            entry_point=entry_point,
        )

    return resolve_from_manifest(entry_point)


def resolve_from_manifest(entry_point):
    """
    Given some entry key from the Vite manifest, returns the html tags that
    should be inserted into the document for that key.

    See: https://vite.dev/guide/backend-integration

    1. A <link rel="stylesheet"> tag for each file in the entry point chunk's
    css list (if it exists)

    2. Recursively follow all chunks in the entry point's imports list and
    include a <link rel="stylesheet"> tag for each CSS file of each imported
    chunk's css list (if it exists).

    3. A tag for the file key of the entry point chunk. This can be <script
    type="module"> for JavaScript, <link rel="stylesheet"> for CSS.

    4. Optionally, <link rel="modulepreload"> tag for the file of each imported
    JavaScript chunk, again recursively following the imports starting from the
    entry point chunk.
    """
    if entry_point not in manifest_data:
        raise ValueError(f"Entry point '{entry_point}' not found in Vite manifest")

    entry = manifest_data[entry_point]
    html = []

    # Assumption: Vite outputs asset paths that are served under Django's STATIC_URL
    # (for example, the Vite build output directory is included in STATICFILES_DIRS).
    # If your Vite build output is not served under STATIC_URL, adjust your Vite build
    # configuration so the manifest file paths resolve correctly relative to STATIC_URL
    # or extend this tag to support a configurable base URL for Vite assets.
    for css_file in entry.get("css", []):
        html.append(stylesheet_tag(css_file))

    def _include_imports(imports):
        for import_entry in imports:
            imported = manifest_data.get(import_entry)
            if not imported:
                continue
            for css_file in imported.get("css", []):
                html.append(stylesheet_tag(css_file))
            if "imports" in imported:
                _include_imports(imported["imports"])

    if "imports" in entry:
        _include_imports(entry["imports"])

    html.append(asset_tag(entry["file"]))

    return mark_safe("\n".join(html))


def asset_tag(file_name):
    file_path = urljoin(settings.STATIC_URL, file_name)
    if is_css_asset(file_name):
        return f'<link rel="stylesheet" href="{file_path}">'

    return f'<script type="module" src="{file_path}"></script>'


def stylesheet_tag(file_name):
    file_path = urljoin(settings.STATIC_URL, file_name)
    return f'<link rel="stylesheet" href="{file_path}">'


def is_css_asset(file_name):
    return file_name.endswith(".css")
