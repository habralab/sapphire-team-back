# Sapphire Storage App

## Preparation

### Migrate

```shell
python -m sapphire storage database migrations apply
```

### Fixtures

```shell
python -m sapphire storage database fixtures apply specializations_groups specializations
```

## Run

```shell
python -m sapphire storage run
```
