import os

DEBUG = False
OUTPUT_DIRECTORY = ''
API_KEY= ''
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JAR_FILES = [
        # Add the path to the jsprit JAR file
        os.path.join(BASE_DIR, 'jar', 'slf4j-api-1.7.32.jar'),  # Add the path to SLF4J JAR
        os.path.join(BASE_DIR, 'jar', "jsprit-core-1.9.0-beta.11.jar"),
        os.path.join(BASE_DIR, 'jar', "logback-core-1.0.11.jar"),
        os.path.join(BASE_DIR, 'jar', "logback-classic-1.0.11.jar"),
        os.path.join(BASE_DIR, 'jar', "jsprit-io-1.9.0-beta.4.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-configuration-1.9.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-lang-2.6.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-logging-1.1.1.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-math-2.1.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-math3-3.4.jar"),
        os.path.join(BASE_DIR, 'jar', "gs-algo-1.3.jar"),
        os.path.join(BASE_DIR, 'jar', "gs-core-1.3.jar"),
        os.path.join(BASE_DIR, 'jar', "gs-ui-1.3.jar"),
        os.path.join(BASE_DIR, 'jar', "hamcrest-core-1.3.jar"),
        os.path.join(BASE_DIR, 'jar', "jcommon-1.0.23.jar"),
        os.path.join(BASE_DIR, 'jar', "jfreechart-1.0.19.jar"),
        os.path.join(BASE_DIR, 'jar', "jsprit-analysis-1.9.0-beta.11.jar"),
        os.path.join(BASE_DIR, 'jar', "junit-4.12.jar"),
        os.path.join(BASE_DIR, 'jar', "xml-apis-1.4.01.jar"),
        os.path.join(BASE_DIR, 'jar', "mbox2-1.0.jar"),
        os.path.join(BASE_DIR, 'jar', "pherd-1.0.jar"),
        os.path.join(BASE_DIR, 'jar', "java-util-1.8.3.jar"),
        os.path.join(BASE_DIR, 'jar', "scala-library-2.10.1.jar"),
        os.path.join(BASE_DIR, 'jar', "xercesImpl-2.12.0.jar"),
        os.path.join(BASE_DIR, 'jar', "xml-apis-1.4.01.jar"),
        ## Graphopper specific librarie
        os.path.join(BASE_DIR, 'jar', "commons-io-1.3.1.jar"),
        os.path.join(BASE_DIR, 'jar', "graphhopper-core-7.0.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-annotations-2.10.5.jar"),
        os.path.join(BASE_DIR, 'jar', "jakarta.activation-api-1.2.1.jar"),
        os.path.join(BASE_DIR, 'jar', "jakarta.xml.bind-api-2.3.2.jar"),
        os.path.join(BASE_DIR, 'jar', "hppc-0.8.1.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-core-2.10.5.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-databind-2.10.5.1.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-dataformat-xml-2.10.5.jar"),
        os.path.join(BASE_DIR, 'jar', "woodstox-core-6.2.1.jar"),
        os.path.join(BASE_DIR, 'jar', "xmlgraphics-commons-2.7.jar"),
        os.path.join(BASE_DIR, 'jar', "commons-compiler-3.1.2.jar"),
        os.path.join(BASE_DIR, 'jar', "graphhopper-web-api-7.0.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-datatype-jts-2.14.jar"),
        os.path.join(BASE_DIR, 'jar', "janino-3.1.2.jar"),
        os.path.join(BASE_DIR, 'jar', "jts-core-1.19.0.jar"),
        os.path.join(BASE_DIR, 'jar', "jackson-module-jaxb-annotations-2.10.5.jar"),
        os.path.join(BASE_DIR, 'jar', "osmosis-osm-binary-0.47.3.jar"),
        os.path.join(BASE_DIR, 'jar', "protobuf-java-3.11.4.jar"),
        os.path.join(BASE_DIR, 'jar', "slf4j-api-1.7.36.jar"),
        os.path.join(BASE_DIR, 'jar', "stax2-api-4.2.1.jar")
]
COLOR_MAP = ["blue", "green", "purple", "orange", "darkred", "lightred", "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "pink", "lightblue", "lightgreen", "gray", "black", "lightgray"]
