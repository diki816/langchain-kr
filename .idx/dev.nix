# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"
  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311Packages.pip
    pkgs.python311Packages.ipykernel
    pkgs.python311
    pkgs.python311Packages.streamlit
  ];
  # Sets environment variables in the workspace
  # env = {
  #   PATH= ["/home/user/.local/bin" ];
  # };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-toolsai.jupyter"
      "ms-python.python"
      "ms-python.debugpy"
      "ms-toolsai.jupyter-keymap"
      "ms-toolsai.jupyter-renderers"
      "ms-toolsai.vscode-jupyter-cell-tags"
      "ms-toolsai.vscode-jupyter-slideshow"
    ];
    workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
      onCreate = {
        create-venv = ''
          python -m venv .venv
          # curl -sSL https://install.python-poetry.org | python -
          source .venv/bin/activate
          pip install -r requirements.txt
        '';
      };
      # To run something each time the environment is rebuilt, use the `onStart` hook
    };
    # Enable previews and customize configuration
    previews = { # The following object sets web previews
      enable = true;
      previews = {
        web = {
          command = [
            "streamlit"
            "run"
            "98-Agent/part4_ch3/app.py"
      #       "--"
      #       "--port"
      #       "$PORT"
      #       "--host"
      #       "0.0.0.0"
            # "--disable-host-check"
          ];
          manager = "web";
      #     # Optionally, specify a directory that contains your web app
      #     # cwd = "app/client";
        };
      };
    };
  };
}

