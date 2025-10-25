from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.stabilizer_code_utilities import get_15_1_3_reed_solomon_code_utilities


class NativeTDistance3:
    def run_main(self):
        target_code = get_15_1_3_reed_solomon_code_utilities()
        SimulateCx(num_cat_states=3, target_code_utilities=target_code, si=0).run_main()


if __name__ == "__main__":
    NativeTDistance3().run_main()
