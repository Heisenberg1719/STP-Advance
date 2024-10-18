import logging, os
from waitress import serve
from app import create_app
from config import ProductionConfig

# Create the app instance with the desired configuration
app = create_app(ProductionConfig)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    threads = int(os.getenv('THREADS', 4)) 
    logger.info(f"Starting server on {host}:{port} with {'debug' if debug_mode else 'production'} mode")
    logger.info(f"Using {threads} threads.")

    try:
        if debug_mode:app.run(host=host, port=port, debug=True)
        else:serve(app, host=host, port=port, threads=threads)
    except KeyboardInterrupt:
        logger.info("Server shutdown initiated by user (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"An error occurred while starting the server: {e}", exc_info=True)
    finally:logger.info("Server has been stopped gracefully.")
