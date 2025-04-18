from cliapp import ApplicationConfig
import json

def main():
    config: ApplicationConfig = ApplicationConfig.fromPath("tests/config.json")
    print()

if __name__ == "__main__":
    main()