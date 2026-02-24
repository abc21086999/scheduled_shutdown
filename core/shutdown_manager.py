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
        hours = self._parse_input(time_input)
        if hours is None:
            self.error_occurred.emit("請輸入有效的數字")
            return

        total_seconds = int(hours * 3600)
        # Avoid scheduling 0 seconds or negative, though _parse_input handles non-numeric
        if total_seconds <= 0:
            self.error_occurred.emit("時間必須大於 0")
            return

        # Execute Windows shutdown command
        # /s = shutdown, /t = time in seconds
        result = subprocess.run(f'shutdown /s /t {total_seconds}', shell=True, capture_output=True)
        if result.returncode == 0:
            # Calculate target time for display
            target_time = datetime.now() + timedelta(seconds=total_seconds)
            self.shutdown_scheduled.emit(target_time)
        elif result.returncode == 1190:
            self.error_occurred.emit("目前已有排程中的關機！")
        else:
            self.error_occurred.emit(f"排程失敗，錯誤碼：{result.returncode}")

    def cancel_shutdown(self):
        """
        Cancels any scheduled shutdown.
        """
        # /a = abort
        result = subprocess.run('shutdown /a', shell=True, capture_output=True)
        if result.returncode == 0:
            self.shutdown_cancelled.emit()
        elif result.returncode == 1116:
            self.error_occurred.emit("目前沒有排程中的關機")
        else:
            self.error_occurred.emit(f"取消失敗，錯誤碼：{result.returncode}")

    def _parse_input(self, string: str):
        """
        Parses the string input into hours.
        Returns None if invalid.
        """
        if not string:
            return None
            
        # Standardize comma to dot just in case
        string = string.replace(',', '.')

        try:
            hour_val = float(string)
            return hour_val
        except ValueError:
            return None
