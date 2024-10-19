import logging,os
from app import create_app
from waitress import serve
from app.utils.appconfig.config import ProductionConfig
from logging.handlers import RotatingFileHandler

app = create_app(ProductionConfig)

# Setup logging
def setup_logging():
    # Set up file handler for logging
    log_file_path = 'app.log'  # You can modify the path as needed
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10 * 1024 * 1024, backupCount=10)
    
    # Set up formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)

    # Capture all log levels
    file_handler.setLevel(logging.NOTSET)
    
    # Add the handler to the root logger (which `logger` will inherit)
    logging.getLogger().addHandler(file_handler)

    # Set up console logging for feedback
    logging.basicConfig(level=logging.INFO)
    
    # Log to the console and file
    logger = logging.getLogger(__name__)
    return logger

# Initialize the logger
logger = setup_logging()

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    threads = os.getenv('THREADS', 4)

    logger.info(f"Starting server in {'debug' if debug_mode else 'production'} mode with {threads} threads.")

    try:
        if debug_mode:
            app.run(host=host, port=port, debug=True)
        else:
            serve(app, host=host, port=port, threads=threads)

    except KeyboardInterrupt:
        logger.info("Server shutdown initiated by user (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"An error occurred while starting the server: {e}", exc_info=True)
    finally:
        logger.info("Server has been stopped gracefully.")
