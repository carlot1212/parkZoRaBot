from string import Template

HARMONIES_QUESTIONS = [Template("How many tree points did $player get?"),
            Template("How many mountain points did $player get?"),
            Template("How many plains points did $player get?"),
            Template("How many building points did $player get?"),
            Template("How many river points did $player get?"),
            Template("How many habitat points did $player get?"),
            Template("How many special habitat points did $player get?"),
            ]

HARMONIES_SCORESHEET = {
    "Tree Points": 0,
    "Mountain Points": 0,
    "Plains Points": 0,
    "Building Points": 0,
    "River Points": 0,
    "Habitat Points": 0,
    "Special Habitat Points": 0,
}
