{
  description = "Selenium Environment";

  inputs = {
    # using nixos-unstable because geckodriver is outdated in nixos-24.05
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:    
      let
        pkgs = import nixpkgs { inherit system; };
      in
      with pkgs;
      {
        devShells.default = mkShell {        
          buildInputs = [ firefox geckodriver ];

          # Somehow VSCode terminal pops up with "bash: __vsc_prompt_cmd_original: command not found"
          shellHook = ''
            unset PROMPT_COMMAND
          '';
        };
      }
    );
}