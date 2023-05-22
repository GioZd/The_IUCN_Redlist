import pandas as pd

WEBSITE = "https://www.iucnredlist.org"

class Animal:
    """
    Animal object allows to easily access DataFrames information

    Class variables
    ---------------
    species: pd.DataFrame
        List of all species with taxonomy and other short information
    names: pd.DataFrame
        List of all animal common names with their scientific name
    assessments: pd.DataFrame
        List of detailed information about all species

    Attributes
    ----------
    name: str
        Scientific name of the animal. If not existing/listed, 
        it is equal to initialization parameter, capitalized
    info: pd.DataFrame
        For internal use. It possibly contains a line of 
        DataFrame species that matches the scientific name
    is_listed: bool
        It is True only if the species is contained in species DataFrame
    ... 
    (all other attributes are created only if the species exists)
        
    Methods
    -------
    get_scientific() -> str
        Finds the scientific name
    get_vernacular() -> str
        Finds the common name
    """
    species = pd.DataFrame({})
    names = pd.DataFrame({})
    assessments = pd.DataFrame({})
    def __init__(self, name: str):
        self.name = self.get_scientific(name)
        self.info = Animal.species.query(f"scientificName == \'{self.name}\'")
        self.is_listed = False if len(self.info) == 0 else True
        if self.is_listed:
            self.vernacular = self.get_vernacular()
            self.kingdom = self.info.loc[self.info.index[0], 'kingdomName']
            self.phylum = self.info.loc[self.info.index[0], 'phylumName']
            self.classis = self.info.loc[self.info.index[0], 'className'] # "class" raises conflictuality
            self.order = self.info.loc[self.info.index[0], 'orderName']
            self.family = self.info.loc[self.info.index[0], 'familyName']
            self.genus = self.info.loc[self.info.index[0], 'genusName']
            self.authority = self.info.loc[self.info.index[0], 'authority']
            self.status = self.info.loc[self.info.index[0], 'redlistCategory']
            self.trend = self.info.loc[self.info.index[0], 'populationTrend']
            self.assessmentId = self.info.loc[self.info.index[0], 'assessmentId']
            self.internalTaxonId = self.info.loc[self.info.index[0], 'internalTaxonId']
            self.url = f"{WEBSITE}/species/{self.internalTaxonId}/{self.assessmentId}"

    def get_scientific(self, name: str) -> str:
        """
        Returns
        -------
        str
            Scientific name if common is given,
            else the capitalized name, supposedly a
            valid scientific name. 
            However, no exeption will be raised 
            if neither are in the datasets
        """
        found = Animal.names.query(f"name == \'{name.title()}\'")
        if len(found) > 0:
            return found.loc[found.index[0], 'scientificName']
        return name.capitalize()

    def get_vernacular(self) -> str | None: 
        """
        Returns
        -------
        str
            English common name, when existing
        """
        if self.is_listed:
            found = Animal.names.query(f"main and scientificName == \'{self.name}\'")
            if(len(found) > 0):
                return found.loc[found.index[0], 'name']
            return self.name

    def __str__(self) -> str:
        if self.is_listed:
            return (
                f"{self.vernacular}\n"
                f"Name: {self.name} {self.authority}\n"
                f"Class: {self.classis}\n"
                f"Order: {self.order}\n"
                f"Family: {self.family}\n"
                f"Conservation: {self.status} ({self.trend})\n"
                f"Info: {self.url}"
            )
        return f"{self.name} (not listed)"
    
# test library
if __name__ == "__main__":
    Animal.species = pd.read_csv("simple_summary.csv")
    Animal.names = pd.read_csv("common_names.csv")
    animal = Animal('Iberian lynx')
    print(animal)