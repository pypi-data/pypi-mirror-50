from mld.smiles_lookup import SmilesLookup


def main():
    smiles_lookup = SmilesLookup()

    result = smiles_lookup.lookup_by_key("ever")
    print(result)


if __name__ == '__main__':
    main()
