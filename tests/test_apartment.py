from pathlib import Path

from apartmentplanner.apartment import Apartment

TMP_RESULT = Path(__file__).parent.resolve() / "tmp_results"


def test_run(resources: Path) -> None:
    apartment = Apartment.from_plan(resources / "rooms.txt")
    apartment.run(output_path=TMP_RESULT / "results.txt")

    assert isinstance(apartment.plan, list)
    assert len(apartment.plan) == 50
    assert len(apartment.walls) == 50
    assert len(apartment.rooms) == 8
    assert apartment.chairs == {"C": 1, "P": 7, "S": 3, "W": 14}
    assert Path(output_path=TMP_RESULT / "results.txt").exists()

    with open(TMP_RESULT / "results.txt", "r", encoding="utf-8") as f:
        result = f.read()

    assert result == ("total:\n"
                      "W: 14, P: 7, S: 3, C: 1\n"
                      "balcony:\n"
                      "W: 0, P: 2, S: 0, C: 0\n"
                      "bathroom:\n"
                      "W: 0, P: 1, S: 0, C: 0\n"
                      "closet:\n"
                      "W: 0, P: 3, S: 0, C: 0\n"
                      "kitchen:\n"
                      "W: 4, P: 0, S: 0, C: 0\n"
                      "living room:\n"
                      "W: 7, P: 0, S: 2, C: 0\n"
                      "office:\n"
                      "W: 2, P: 1, S: 0, C: 0\n"
                      "sleeping room:\n"
                      "W: 1, P: 0, S: 1, C: 0\n"
                      "toilet:\n"
                      "W: 0, P: 0, S: 0, C: 1\n")
