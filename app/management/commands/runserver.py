import atexit
import os
import signal
import subprocess
import sys
from daphne.management.commands.runserver import Command as DaphneRunserverCommand
from django.conf import settings


class Command(DaphneRunserverCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vite_process = None

    def handle(self, *args, **options):
        # Check if dev_mode is enabled
        vite_config = settings.DJANGO_VITE.get("default", {})
        dev_mode = vite_config.get("dev_mode", False)
        dev_command = getattr(settings, "DJANGO_VITE_DEV_COMMAND", None)

        # Only start Vite in the main autoreloader process (not the worker)
        # or when autoreload is disabled
        use_reloader = options.get("use_reloader", True)
        is_main_process = os.environ.get("RUN_MAIN") != "true"

        if dev_mode and dev_command and (not use_reloader or is_main_process):
            self.start_vite(dev_command)

        # Call parent's handle to start Django
        super().handle(*args, **options)

    def start_vite(self, command):
        """Start Vite dev server as subprocess"""
        try:
            self.stdout.write(f"Starting Vite dev server: {command}")
            self.vite_process = subprocess.Popen(
                command.split(),
                stdout=sys.stdout,
                stderr=sys.stderr,
            )

            # Register cleanup handlers
            atexit.register(self.stop_vite)
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)

        except FileNotFoundError:
            self.stderr.write(
                self.style.ERROR(
                    f"Failed to start Vite: Command '{command}' not found. "
                    f"Make sure Node.js and pnpm are installed."
                )
            )
            sys.exit(1)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to start Vite dev server: {e}"))
            sys.exit(1)

    def stop_vite(self):
        """Stop Vite dev server"""
        if self.vite_process:
            self.vite_process.terminate()
            try:
                self.vite_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.vite_process.kill()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.stop_vite()
        sys.exit(0)
