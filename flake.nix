{
  description = "Python Static Site Generator";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        buildScript = pkgs.writeScriptBin "build" ''
          #!${pkgs.bash}/bin/bash
          PYTHONPATH=$PYTHONPATH:. ${pkgs.python312}/bin/python3 -m src.main
        '';

        testScript = pkgs.writeScriptBin "tests" ''
          #!${pkgs.bash}/bin/bash
          PYTHONPATH=$PYTHONPATH:. ${pkgs.python312}/bin/python3 -m unittest discover -s tests
        '';

        serveScript = pkgs.writeScriptBin "serve" ''
          #!${pkgs.bash}/bin/bash

          print_error() {
            echo "''$(tput setaf 1)''$(tput bold)Error:''$(tput sgr0) $1" >&2
          }

          check_public_directory() {
            if [ ! -d "public" ] || [ -z "$(ls -A public 2>/dev/null)" ]; then
              print_error "directory 'public' does not exist or is empty."
              echo "    Run 'build' before running 'serve'"
              return 1
            fi

            return 0
          }

          serve_public_directory() {
            echo "Starting HTTP server on 0.0.0.0 port 8888 (http://0.0.0.0:8888/)"
            cd public && ${pkgs.python312}/bin/python3 -m http.server 8888
          }

          if check_public_directory; then
            serve_public_directory
          else
            exit 1
          fi
        '';

        formatScript = pkgs.writeScriptBin "format" ''
          #!${pkgs.bash}/bin/bash

          show_usage() {
            echo "Format Python code using Black"
            echo "Usage:"
            echo "  * format check - Check file formatting"
            echo "  * format fix - Format all files in project"
          }

          case "$1" in
            "check")
              ${pkgs.black}/bin/black --check .
              ;;
            "fix")
              ${pkgs.black}/bin/black .
              ;;
            *)
              show_usage
              ;;
          esac
        '';

        mainPackage = pkgs.writeScriptBin "site-generator" ''
          #!${pkgs.bash}/bin/bash
          PYTHONPATH=$PYTHONPATH:. ${pkgs.python312}/bin/python3 -m src.main
          echo "Starting HTTP server on 0.0.0.0 port 8888 (http://0.0.0.0:8888/)"
          cd public && ${pkgs.python312}/bin/python3 -m http.server 8888
        '';
      in
      {
        packages.default = mainPackage;

        devShells.default = pkgs.mkShell {
          packages = [ pkgs.zsh ];
          buildInputs = [
            pkgs.python312
            pkgs.black
            pkgs.pyright
            buildScript
            testScript
            serveScript
            formatScript
          ];

          shellHook = ''
            export SHELL=${pkgs.zsh}/bin/zsh

            echo "Development environment loaded!"
            echo "Available commands:"
            echo "  * build - Generate the static site"
            echo "  * tests - Execute unit tests"
            echo "  * serve - Serve the site at port 8888"
            echo "  * format check - Check file formatting"
            echo "  * format fix - Format files in project"

            if [[ $SHELL != ${pkgs.zsh}/bin/zsh ]]; then
              exec ${pkgs.zsh}/bin/zsh
            fi
          '';
        };
      });
}
