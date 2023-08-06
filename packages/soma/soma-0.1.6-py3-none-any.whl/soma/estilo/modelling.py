import numpy as np
from typing import List, Tuple
import pandas as pd


def correlation_matrix(m: np.ndarray, labels: List[str] = None) -> np.ndarray:
    """
        Calculates a correlation matrix given a :math:`[N_{samples} \\times N_{features}]` data matrix.
        
        This correlation is composed of the Pearson Correlation Coefficient
        between each pair of features.

        Args:
            m (:class:`numpy.ndarray`): 
                A :math:`[N_{samples} \\times N_{features}]` data matrix.
            labels (list(str)): 
                A list of n_features labels.

        Returns:
            :class:`numpy.ndarray`: The resulting :math:`[N_{features} \\times N_{features}]` correlation matrix.
    """
    corr_matrix = np.corrcoef(m)

    return corr_matrix


def distance_matrix(m: np.ndarray) -> np.ndarray:
    """
        Calculates a :math:`[N_{samples} \\times N_{samples}]` distance matrix given a :math:`[N_{samples} \\times N_{features}]` data matrix. 

        Args:
            m (:class:`numpy.ndarray`): A :math:`[N_{samples} \\times N_{features}]` data matrix.

        Returns:
            :class:`numpy.ndarray`: The resulting :math:`[N_{samples} \\times N_{samples}]` distance matrix.
    """
    from scipy.spatial.distance import pdist, squareform

    dist_matrix = squareform(pdist(m))

    return dist_matrix


def distance_sorter(dist_matrix: np.ndarray) -> Tuple[np.array, np.array]:
    """
        Calculates an sorted total distance (useful for finding outliers) and plots it.
        
        Args:
            dist_matrix (:class:`numpy.ndarray`): A [N x N] distance matrix.
        
        Returns:
            (tuple): Tuple contaning:
                - dists (:class:`numpy.ndarray`): Total distance for each sample.
                - i_dists (:class:`numpy.ndarray`): Indexes used to sort dists.
    """
    dists = np.sum(dist_matrix, axis=1)

    i_dists = np.argsort(dists)
    dists_sorted = dists[i_dists]

    return i_dists, dists_sorted


def count_unique_votes(df: pd.DataFrame) -> pd.DataFrame:
    """
        Counts amount of each vote for all products.

        Args:
            df (:class:`pandas.Dataframe`): The voting df with all votes for each product.
        Returns:
            :class:`pandas.Dataframe`: The original dataframe with additional columns for each note
            and their count
    """

    # Checks for the necessary columns in the dataframe
    if "id_produto_cor" not in df.columns:
        print("Dataframe does not contain id_produto_cor key column")
        return -1
    if "nota" not in df.colums:
        print("Dataframe does not contain id_produto_cor key column")
        return -2

    # Finding all different notes
    notes_list = df["nota"].unique().apply(lambda x: "C" + str(x)).tolist()

    d = {}
    for id in df["id_produto_cor"].unique():
        count = df[df["id_produto_cor"] == id]["nota"].value_counts(sort=False).T
        d[id] = count.to_numpy()

    return (
        pd.DataFrame.from_dict(d, orient="index", columns=notes_list)
        .reset_index()
        .rename(columns={"index": "id_produto_cor"})
        .replace(np.nan, 0)
    )


def consolidate_votes(
    merged_df: pd.DataFrame, dados_animale: pd.DataFrame
) -> pd.DataFrame:
    """
        Merges the sales+notes dataset with statistical measures for nota and nota_preco.

        Args:
            merged_df (:class:`pandas.Dataframe`): Sales data with repeating product, each with nota and nota_preco.
            dados_animale (:class:`pandas.Dataframe`): Sales data with all products.
        Returns:
            :class:`pandas.Dataframe`: The resulting merged Dataframe.
    """

    labels = ["nota", "nota_preco"]
    dados_agg = (
        merged_df[["id_produto_cor"] + labels]
        .groupby("id_produto_cor")
        .agg([np.mean, np.std, len])
    )

    dados_agg.columns = list(map("".join, dados_agg.columns.values))
    dados_agg = dados_animale.merge(dados_agg, on="id_produto_cor")

    dados_agg = dados_agg.merge(count_unique_votes(merged_df), on="id_produto_cor")

    return dados_agg
