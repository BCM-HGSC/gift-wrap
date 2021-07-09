# gift-wrap

A collection of wrappers used by the Submissions Team.

Currently a work in progress, done in the background after other priority work.


## To Run
The only thing available is Sample Tracker and its tests.

With Poetry
- `poetry install .[sample_tracker]`
- `pytest`

Without Poetry
- `cd to/directory`
- `pip install .[sample_tracker]`
- `pytest # You have to install this since right now, pip install . doesn't install poetry dev-dependencies`

## Future
- Planning to add more wrappers
- Planning where you can modular install the ones you need (so you dont install dxpy if you dont need it)
- Maybe switch away from poetry

