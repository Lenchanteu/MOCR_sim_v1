class Console:

    DEFAULT_CONSOLES = {

        "FD": "Flight Director",

        "GNC": "Guidance Navigation Control",

        "PROP": "Propulsion",

        "EPS": "Electrical Power System",

        "COMM": "Communications",

        "ECLSS": "Life Support"

    }


    @staticmethod
    def get_all():

        return Console.DEFAULT_CONSOLES