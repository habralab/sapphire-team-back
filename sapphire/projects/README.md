# Sapphire Projects App

## Preparation

### Migrate

```shell
python -m sapphire projects database migrations apply
```

### Fixtures
```shell
python -m sapphire projects database fixtures apply projects positions participants
```

## Run

```shell
python -m projects run
```
