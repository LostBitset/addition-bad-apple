Build {
	Units = function()
		local fsrs = Program {
			Name = "FSRS",
			Sources = { "main.cc" },
		}
		Default(fsrs)
	end,
	Configs = {
		Config {
			Name = "linux-gcc",
			DefaultOnHost = "linux",
			Tools = { "gcc" },
			Env = {
				PROGOPTS = "-lstdc++",
			},
		},
	},
}

