# Sapphire Notifications App

## Preparation

### Migrate

```shell
python -m sapphire notifications database migrations apply 
```

### Fixtures
```shell
python -m sapphire notifications database fixtures apply autotests
```

## Run

```shell
python -m sapphire notifications run
```
