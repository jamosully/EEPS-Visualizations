import EEPS.initialization_detail as env_d
import json

def translate_env_detail_2_json(json_filename):

    experiment_details = env_d.environment_details()
    json_dictionary = {}

    for experiment_id in experiment_details.keys():
        new_exp_dic = {}
        for parameter in experiment_details[experiment_id].keys():
            if parameter == "training_order":
                new_exp_dic["training_order"] = {}
                for phase in experiment_details[experiment_id][parameter].keys():
                    new_exp_dic["training_order"][str(phase)] = []
                    for step in experiment_details[experiment_id][parameter][phase]:
                        step_dic = {
                            "sample": step[0],
                            "comparison": step[1],
                            "repeat_num": step[2]
                        }
                        new_exp_dic["training_order"][str(phase)].append(step_dic)
            else:
                new_exp_dic[parameter] = experiment_details[experiment_id][parameter]
        new_exp_dic["description"] = ""
        json_dictionary[str(experiment_id)] = new_exp_dic

    with open(json_filename, "w") as json_file:
        json.dump(json_dictionary, json_file, indent=4)

translate_env_detail_2_json("test.json")