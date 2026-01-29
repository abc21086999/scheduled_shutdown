import subprocess
from datetime import datetime, timedelta
from PySide6.QtCore import QObject, Signal

class ShutdownManager(QObject):
    """
    Manages shutdown logic and communicates with the UI via Signals.
    """
    # Signals to notify the UI of status changes
    shutdown_scheduled = Signal(datetime)  # Emitted when shutdown is successfully scheduled (payload: target time)
    shutdown_cancelled = Signal()          # Emitted when shutdown is cancelled
    error_occurred = Signal(str)           # Emitted when there is an input error (payload: error message)

    def schedule_shutdown(self, time_input: str):
        """
        Parses input and schedules a shutdown if valid.
        """
        hours, minutes = self._parse_input(time_input)
        
        if hours is None:
            self.error_occurred.emit("請輸入有效的數字")
            return

        total_seconds = int(hours * 3600 + minutes * 60)
        
        # Avoid scheduling 0 seconds or negative, though _parse_input handles non-numeric
        if total_seconds <= 0:
            self.error_occurred.emit("時間必須大於 0")
            return

        try:
            # Execute Windows shutdown command
            # /s = shutdown, /t = time in seconds
            subprocess.run(f'shutdown /s /t {total_seconds}', shell=True, check=True)
            
            # Calculate target time for display
            target_time = datetime.now() + timedelta(seconds=total_seconds)
            self.shutdown_scheduled.emit(target_time)
            
        except subprocess.CalledProcessError as e:
            # This might happen if a shutdown is already in progress
            self.error_occurred.emit(f"指令執行失敗 (可能已有倒數中): {e}")
        except Exception as e:
            self.error_occurred.emit(f"發生未預期的錯誤: {e}")

    def cancel_shutdown(self):
        """
        Cancels any scheduled shutdown.
        """
        try:
            # /a = abort
            subprocess.run('shutdown /a', shell=True, check=True)
            self.shutdown_cancelled.emit()
        except subprocess.CalledProcessError:
            # If no shutdown was in progress, Windows might return an error code for /a.
            # We can treat this as "cancelled anyway" or just ignore.
            # For UI feedback, we still emit cancelled.
            self.shutdown_cancelled.emit()
        except Exception as e:
            self.error_occurred.emit(f"取消失敗: {e}")

    def _parse_input(self, string: str):
        """
        Parses the string input into (hours, minutes).
        Returns (None, None) if invalid.
        """
        if not string:
            return None, None
            
        # Standardize comma to dot just in case
        string = string.replace(',', '.')

        if string.isnumeric():
            return int(string), 0
        else:
            try:
                hour_val = float(string)
                integer, decimal = divmod(hour_val, 1)
                return int(integer), int(round(decimal * 60))
            except ValueError:
                return None, None
