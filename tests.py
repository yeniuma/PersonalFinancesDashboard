import pytest
import pandas as pd

from data_cleaning import get_raw_excels_as_dataframe


@pytest.mark.parametrize(
    "excels_to_process,processed_excels",
    [([], []), (["processed_file"], ["processed_file"])],
)
def test__get_raw_excels_as_dataframe__nothing_to_process__returns_none(
    excels_to_process, processed_excels
):
    assert (
        get_raw_excels_as_dataframe(
            excels_to_process=excels_to_process, processed_excels=processed_excels
        )
        is None
    )


def test__get_raw_excels_as_dataframe__raw_and_processed_file_mix__returns_raw_rows_concatted(
    tmp_path,
):
    to_process = [
        tmp_path / "not_processed_yet.xlsx",
        tmp_path / "also_not_processed.xlsx",
        tmp_path / "already_processed.xlsx",
    ]
    processed_excels = [tmp_path / "already_processed.xlsx"]
    pd.DataFrame({"col": [1, 2]}).to_excel(to_process[0], index=False)
    pd.DataFrame({"col": [3, 4]}).to_excel(to_process[1], index=False)
    pd.DataFrame({"col": [666, 666]}).to_excel(to_process[2], index=False)
    expected_values = [1, 2, 3, 4]

    result = get_raw_excels_as_dataframe(
        excels_to_process=to_process, processed_excels=processed_excels
    )

    assert result.values.all() in expected_values
