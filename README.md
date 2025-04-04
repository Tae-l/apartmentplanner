# ApartmentPlanner

Solution to the problem described in `task_en.txt`

## How to run ?

### From terminal

Install the package with: 

```bash
pip install -e
```

Then run

```bash
python main.py --plan "path_to_rooms.txt" --output "path_to_output.txt"
```

### From IDE

Run `scripts_run_chairs.py` in `/scripts/` directly from an IDE. 
Result will be placed in `/scripts/results/result.txt`

### From tests 

Install dev requirements with 

```bash
pip install -e
```
or 
```bash
pip install -r requirements_dev.txt
```

Then run `/tests/tests_apartment.py`. 
Result will be placed in `/tests/tmp_results/result.txt`

