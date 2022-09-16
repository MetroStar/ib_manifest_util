# Website

This website is built using [Docusaurus 2](https://docusaurus.io/), a modern static website generator. The following
commands must be run from the `documentation` directory.

## Building the docs locally

### Installation

```
$ yarn install
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Publishing the docs

We are publishing docs using the `gh-pages` mechanism that's built into GitHub (thanks GitHub!). As such,  we have a
dedicated `gh-pages` branch from which the docs are served.

When a PR is opened which makes changes to files in the documentation folder, the `Test Deployment` Action will run.

When a PR is merged into `dev` or `main`, the `Test Deployment` Action and the `Publish Docs` Action will run. The
`Publish Docs` Action will build the Docusaurus website files and push them to the `gh-pages` branch. GitHub will
then detect changes to the `gh-pages` branch and trigger its own deploy workflow.
