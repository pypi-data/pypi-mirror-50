import logging
from logging import handlers

from cloud_storage_provider import constants


def set_log_handlers(logger):
	if logger.hasHandlers():
		return

	# Create handlers and set their log levels
	logger.setLevel(logging.DEBUG)

	rotating_file_handler = handlers.RotatingFileHandler(
		filename=constants.LOG_NAME,
		maxBytes=10000,
		backupCount=5,
		encoding='utf-8'
	)
	rotating_file_handler.setLevel(logging.WARNING)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.DEBUG)

	# Create formatters for the logs
	stream_log_format = logging.Formatter(
		"%(asctime)s - %(name)s - %(levelname)s: %(message)s")
	file_log_format = logging.Formatter(
		"%(asctime)s - %(name)s - %(levelname)s: %(message)s")
	stream_handler.setFormatter(stream_log_format)
	rotating_file_handler.setFormatter(file_log_format)

	# Attach handlers to logger
	logger.addHandler(rotating_file_handler)
	logger.addHandler(stream_handler)


def get_logger():
	app_logger = logging.getLogger("CLOUD STORAGE PROVIDER")
	set_log_handlers(app_logger)

	return app_logger
