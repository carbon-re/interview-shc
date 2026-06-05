import pandas as pd

def csvParser(filepath: str) -> list[dict]:
    return pd.read_csv(filepath)

def calculateIndividualValue(sil_tput, coal_tput, coal_ncv):
    CLINKER_RATIO = 1.55

    heat = coal_tput*coal_ncv
    clinker_mass = sil_tput/CLINKER_RATIO

    return heat/clinker_mass

def appendShcColumn(df: pd.DataFrame, timestamp_col: str, sil_tput: str, coal_tput: str, coal_ncv: str) -> pd.DataFrame:
    df["shc"] = df.apply(
        lambda row: calculateIndividualValue(row[sil_tput], row[coal_tput], row[coal_ncv]), axis=1
    )
    return df

def formatOutput(df):
    #return df[["timestamp", "shc"]].to_dict(orient="records")
    return dict(zip(df["timestamp"], df["shc"]))

def main():
    # harcode path. delete me
    loc = "src/python/soft_sensors/test_data/abc.csv"

    data = csvParser(loc)
    print(data)
    
    newData=appendShcColumn(data, "timestamp", "s_ph_sil_tput", "f_k_coal_tput", "f_k_coal_ncv")

    out = formatOutput(newData)
    print(out)
    return out

if __name__ == "__main__":
    main()