FROM nixos/nix

WORKDIR /usr/src/app

RUN nix-env -iA cachix -f https://cachix.org/api/v1/install
RUN cachix use devenv
RUN nix-env -if https://install.devenv.sh/latest
RUN nix-env -iA nixpkgs.direnv

ADD devenv.nix devenv.nix
ADD devenv.yaml devenv.yaml
ADD devenv.lock devenv.lock
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

RUN devenv ci

RUN devenv shell pipenv install --dev

ADD . .

ENTRYPOINT ["devenv", "shell", "bash", "scrambled-strings"]
