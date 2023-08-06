from ifm import Enum


class DfePd:
    """
    Functions for exporting dfe properties to DataFrames.
    """

    def __init__(self, doc):
        self.doc = doc

    def dfe(self):
        import pandas as pd
        import numpy as np

        df_nodes = self.doc.c.mesh.df.nodes()

        df_dfe = pd.DataFrame(
            [self.doc.getNodalArrayOfFractureElement(f) for f in range(self.doc.getNumberOfTotalFractureElements())],
            columns=["node_1", "node_2"])
        df_dfe.index.name = "dfe"
        df_dfe["Law"] = [self.doc.getFracLaw(f, Enum.FRAC_1D, Enum.ALL_FRAC_MODES) for f in
                         range(self.doc.getNumberOfTotalFractureElements())]

        # df_dfe["Area"] = [doc.getFracArea(f, Enum.FRAC_1D, Enum.ALL_FRAC_MODES) for f in range(doc.getNumberOfTotalFractureElements())]

        df_dfe["x1"] = np.array(df_nodes.loc[df_dfe.node_1].X)
        df_dfe["x2"] = np.array(df_nodes.loc[df_dfe.node_2].X)
        df_dfe["y1"] = np.array(df_nodes.loc[df_dfe.node_1].Y)
        df_dfe["y2"] = np.array(df_nodes.loc[df_dfe.node_2].Y)
        df_dfe["length"] = ((df_dfe.x1 - df_dfe.x2) ** 2 + (df_dfe.y1 - df_dfe.y2) ** 2) ** 0.5

        return df_dfe
