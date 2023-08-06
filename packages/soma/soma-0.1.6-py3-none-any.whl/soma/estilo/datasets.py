#%%
from soma.estilo import modelling, utils
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import os

class Datasets:
    def __init__(self):
        self.train = None
        self.test = None
        self.path = None
        self.desc = None
        self.label_columns = None
        self.dataset = None

    def load_sales(
        self,
        encoder=None,
        train_collections=["VER18", "INV18"],
        test_collections=["VER19"],
        clf=False,
    ):

        try:
            with open(os.environ.get('SALES_DATASET_PATH'), "rb") as f:
                dataset = pd.read_pickle(f)
        except:
            dataset = self.create_sales()

        col = [
            "qtde",
            "linha",
            "grupo",
            "preco",
            "disc",
            "category",
            "apparel",
            "productpatern",
            "product",
            "bodygarment",
            "giro",
        ]

        train_mask = dataset["colecao"].isin(train_collections)
        test_mask = dataset["colecao"].isin(test_collections)
        
        self.dataset = dataset

        if clf:
            top_giro = dataset[train_mask]['giro'].mean() + dataset[train_mask]['giro'].std()*0.5
            bot_giro = dataset[train_mask]['giro'].mean() - dataset[train_mask]['giro'].std()*0.5
            dataset['giro'] = dataset['giro'].apply(lambda x: 1*(x > top_giro) + 2*(x < bot_giro))
            self.type = 'CLF'
        else:
            self.type = 'REG'

        dataset = dataset[col]

        if encoder:
            encoder = encoder(cols=list(set(self.label_columns) & set(col)))
            dataset = encoder.fit_transform(dataset)
            self.desc = 'Encoded_dataset'

        dataset_train = dataset[train_mask][:]
        dataset_test = dataset[test_mask][:]

        self.train = (dataset_train.to_numpy()[:,:-1], dataset_train.to_numpy()[:,-1])
        self.test = (dataset_test.to_numpy()[:,:-1], dataset_test.to_numpy()[:,-1])
        self.desc = 'Labelled_dataset'

        return self

    def create_sales(self):
        path_animale = os.environ.get('ANIMALE_SALES_PATH')
        path_tags = os.environ.get('ANIMALE_TAGS_PATH')

        try:
            fixed_tags = pd.read_pickle(path_tags)
        except:
            with open("tags_query.sql", "r") as f:
                query = f.read()
            tags = utils.connect_and_query(query)

            tags = tags.groupby("id_produto_cor").apply(
                lambda x: x["desc_Fashion_Attributes"].str.cat(sep=",")
            )
            tags = pd.DataFrame(tags).reset_index()
            tags.columns = ["id", "nome"]
            tags = tags.set_index("id")
            split_tags = tags["nome"].str.split(",", expand=True)
            split_tags = split_tags.set_index(tags.index.values)

            fixed_tags = utils.reorganize_tags(split_tags).reset_index()
            fixed_tags.rename(
                columns={fixed_tags.columns[0]: "id_produto_cor"}, inplace=True
            )

            with open(path_tags, "wb") as f:
                pickle.dump(fixed_tags, f)

        try:
            animale_df = pd.read_pickle(path_animale)
        except:
            print("File Doesn't exist")
            return 0

        animale_df = utils.clean_animale_dataset(animale_df)
        animale_df.rename(columns={"preco_varejo_original": "preco"}, inplace=True)
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "SAPATOS"].index, inplace=True
        )
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "SAPATILHA"].index, inplace=True
        )
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "BOLSAS"].index, inplace=True
        )
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "DIVERSOS"].index, inplace=True
        )
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "CINTOS"].index, inplace=True
        )
        animale_df.drop(
            animale_df.loc[animale_df["grupo"] == "ACESSORIOS"].index, inplace=True
        )

        animale_df = animale_df.merge(fixed_tags, on="id_produto_cor")
        animale_df.reset_index(inplace=True, drop=True)
        animale_df.drop(
            [
                "bag",
                "clutch",
                "sneakers",
                "sandal",
                "boots",
                "sandals",
                "heel",
                "footwear",
                "shoe",
                "shoes",
                "toe",
            ],
            axis=1,
            inplace=True,
        )

        animale_df["grupo"].replace(r"^(TOP) (.*)", r"\1", regex=True, inplace=True)
        animale_df["grupo"].replace(r"^(OVERTOP)(.*)", r"\1", regex=True, inplace=True)

        animale_df["bodygarment"] = (
            animale_df["lowerbodygarment"].astype(str)
            + animale_df["upperbodygarment"].astype(str)
            + animale_df["fullbodygarment"].astype(str)
        )
        animale_df["bodygarment"].replace(
            r"^None(.*)None", r"\1", regex=True, inplace=True
        )
        animale_df.drop(
            columns=["lowerbodygarment", "upperbodygarment", "fullbodygarment"],
            inplace=True,
        )
        animale_df[animale_df.columns[11:]] = animale_df[
            animale_df.columns[11:]
        ].astype(str)

        self.label_columns = ["linha", "grupo"] + animale_df.columns[11:].to_list()

        for col in self.label_columns:
            animale_df[col] = utils.label_encode_col(animale_df[col])

        with open(os.environ.get('SALES_DATASET_PATH'), "wb") as f:
            pickle.dump(animale_df, f)

        return animale_df

