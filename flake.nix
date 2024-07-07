{
  description = "Development environment with Python 3.12 and Poetry";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }: 
    flake-utils.lib.eachDefaultSystem (system: 
      let 
        pkgs = import nixpkgs { 
          inherit system; 
        }; 
      in 
      { 
        devShell = pkgs.mkShell { 
          buildInputs = [ 
            pkgs.python312Full 
            pkgs.poetry 
          ];

          shellHook = ''
            export POETRY_VIRTUALENVS_IN_PROJECT=true
          '';
        };
      });
}