{ pkgs, ... }:

{
  env.PIPENV_VERBOSITY = -1;
  env.PYTHONPATH = "scrambled_word_matcher";

  packages = with pkgs; [
    python311Packages.python
    python311Packages.pip
    pipenv
  ];

  # enterShell = ''
  #   echo "Hello, fellow hacker!"
  #   python --version
  # '';
}
