import matplotlib.pyplot as plt


def _ocorrencias_por_genero(df, genero):
    df_ocorrencias_por_genero = df.loc[
        (df["Gender"] == genero)
        & (df["Medical Condition"].notna())
        & (df["Gender"].notna()),
        ["Gender", "Medical Condition"],
    ]
    return df_ocorrencias_por_genero


def maiores_ocorrencias_por_genero(df, genero):
    df_ocorrencias_por_genero = _ocorrencias_por_genero(df, genero)
    maiores_ocorrencias = (
        df_ocorrencias_por_genero.groupby("Medical Condition")
        .value_counts()
        .nlargest(10)
    )
    return maiores_ocorrencias


def segmentacao_por_entrada_em_hospitais(df, pd, admissao, numero_indicadores):
    tipos_de_entradas = df["Admission Type"].unique().tolist()
    hospitais_segmentados_por_entradas = (
        df[["Admission Type", "Hospital"]]
        .value_counts()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={0: "Counts"})
    )
    dados_filtrados = []
    hospitais_segmentados_por_entradas
    for entrada in tipos_de_entradas:
        filtragem = hospitais_segmentados_por_entradas.query(
            f"`Admission Type` == '{entrada}'"
        )
        dados_filtrados.append(filtragem)

    dataframe_hospitais_segmentados = pd.concat(dados_filtrados, ignore_index=True)

    return dataframe_hospitais_segmentados.query(
        f"`Admission Type`== '{admissao}'"
    ).nlargest(numero_indicadores, "count")


def grafico_entradas_por_hospital(df, admissao, numero_indicadores):
    filtro_admissao = (df["Admission Type"] == admissao) & (df["Hospital"].notna())
    quantidade_de_entradas = (
        df.loc[filtro_admissao, ["Admission Type", "Hospital"]]
        .value_counts()
        .nlargest(numero_indicadores)
    )
    dataframe = quantidade_de_entradas.reset_index(name="Count")
    dataframe.set_index(["Admission Type", "Hospital"])["Count"].plot(
        kind="pie",
        autopct="%1.1f%%",
        figsize=(7, 7),
        title="Distribuição por maiores entradas em hospitais",
    )

    plt.ylabel("")
    plt.show()
