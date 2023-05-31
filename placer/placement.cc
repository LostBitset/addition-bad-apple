#include <vector>
#include <utility>

#include "netlist.cc"

struct PlacedGate {
	Gate gate;
	int x;
	int y;

	public:
		std::string preview() {
			std::string xy = "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
			std::string gate_line = gate.as_line();
			return "PlacedGate at " + xy + ", containing " + gate_line;
		}

		std::string text() {
			std::string xy = std::to_string(x) + "," + std::to_string(y);
			std::string gate_line = gate.as_line();
			return gate_line + " @ " + xy;
		}
};

class Placement {
	public:
		Placement(std::vector<PlacedGate> arg_items)
			: items{arg_items}
			{}

		std::string preview_all() {
			std::string result = "";
			bool first = true;
			for (PlacedGate item : items) {
				if (!first) result += "\n";
				result += item.preview();
				first = false;
			}
			return result;
		}

		std::string text_all() {
			std::string result = "";
			bool first = true;
			for (PlacedGate item : items) {
				if (!first) result += "\n";
				result += item.text();
				first = false;
			}
			return result;
		}

		static Placement from_netlist_naive(Netlist netlist, int sizex, int sizey) {
			int total_size = (sizex - 1) * (sizey - 1);
			int gate_size = total_size / netlist.n_gates();
			std::vector<PlacedGate> items;
			int curr_x = 0;
			int curr_y = 0;
			for (Gate gate : netlist.get_gates()) {
				items.push_back(PlacedGate{
					gate,
					curr_x,
					curr_y,
				});
				curr_x += gate_size;
				if (curr_x > (sizex - 1)) {
					curr_x = 0;
					curr_y += gate_size;
				}
			}
			return Placement(items);
		}

	protected:
		std::vector<PlacedGate> items;
		int sizex;
		int sizey;
};

