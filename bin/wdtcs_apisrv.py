from eve import Eve
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WDTCS Api Server')
    parser.add_argument('SETTINGS_PATH', help="Path to the settings file.")

    # process the command line arguments
    args = parser.parse_args()

    # Start the API server up 
    app = Eve(settings=args.SETTINGS_PATH)
    app.run()

