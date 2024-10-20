import logging,os
from app import create_app
from waitress import serve
from app.utils.appconfig.config import ProductionConfig
from logging.handlers import RotatingFileHandler

app = create_app(ProductionConfig)

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s: %(message)s',
handlers=[logging.FileHandler("app.log"),logging.StreamHandler()])

if __name__ == '__main__':

    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    threads = os.getenv('THREADS', 4)

    logging.info(f"Starting server in {'debug' if debug_mode else 'production'} mode with {threads} threads.")

    try:
        
        if debug_mode:app.run(host=host, port=port, debug=True)
        else:serve(app, host=host, port=port, threads=threads)

    except KeyboardInterrupt:
        logging.info("Server shutdown initiated by user (KeyboardInterrupt).")
    except Exception as e:
        logging.error(f"An error occurred while starting the server: {e}", exc_info=True)
    finally:logging.info("Server has been stopped gracefully.")
