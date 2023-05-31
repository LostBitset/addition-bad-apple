#include <exception>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

typedef int Wire;

struct Gate {
	std::string name;
	std::vector<Wire> inputs;
	std::vector<Wire> outputs;

	public:
		std::string as_line() {
			std::string all_inputs;
			if (inputs.size() > 0) {
				all_inputs = std::accumulate(
					std::next(inputs.begin()),
					inputs.end(),
					std::to_string(inputs[0]),
					[](std::string a, Wire x) -> std::string {
						return a + " " + std::to_string(x);
					}
				) + " ";
			} else {
				all_inputs = "";
			}
			std::string all_outputs;
			if (outputs.size() > 0) {
				all_outputs = " " + std::accumulate(
					std::next(outputs.begin()),
					outputs.end(),
					std::to_string(outputs[0]),
					[](std::string a, Wire x) -> std::string {
						return a + " " + std::to_string(x);
					}
				);
			} else {
				all_outputs = "";
			}
			return name + " " + all_inputs + "~>" + all_outputs;
		}

		static Gate from_line(std::string line) {
			std::string name;
			std::vector<Wire> inputs;
			std::vector<Wire> outputs;
			std::istringstream iss (line);
			std::string tok;
			bool at_name = true;
			bool at_inputs = true;
			while (std::getline(iss, tok, ' ')) {
				if (at_name) {
					name = tok;
					at_name = false;
					continue;
				}
				if (tok == "~>") {
					at_inputs = false;
					continue;
				}
				if (at_inputs) {
					inputs.push_back(std::stoi(tok));
				} else {
					outputs.push_back(std::stoi(tok));
				}
			}
			Gate gate {name, inputs, outputs};
			return gate;
		}
};

class exntype_nonetlisterror : public std::exception {
	virtual const char* what() const throw() {
		return "Unable to find netlist.";
	}
} NoNetlistError;

class Netlist {
	public:
		Netlist(std::vector<Gate> arg_gates)
			: gates{arg_gates}
			{}

		std::vector<Gate> get_gates() {
			return gates;
		}

		unsigned int n_gates() {
			return gates.size();
		}

		std::string preview() {
			unsigned int ng = n_gates();
			if (ng > 0) {
				return "Netlist with " + std::to_string(ng) + " gates, first is \"" + gates[0].as_line() + "\".";
			} else {
				return "Netlist with no gates.";
			}
		}

		static Netlist from_file(std::string filename) {
			std::vector<Gate> gates;
			std::ifstream file (filename);
			std::string line;
			if (file.is_open()) {
				while (std::getline(file, line)) {
					gates.push_back(Gate::from_line(line));
				}
				file.close();
			} else {
				std::cout << "ERROR | Unable to open to open netlist file." << std::endl;
				throw NoNetlistError;
			}
			return Netlist(gates);
		}

	protected:
		std::vector<Gate> gates;
};

