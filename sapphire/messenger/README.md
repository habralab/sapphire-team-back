# Sapphire Messenger App

## Preparation

### Migrate

```shell
python -m sapphire messenger database migrations apply
```

### Fixtures

```shell
python -m sapphire messenger database migrations fixtures apply autotests
```

## Run

```shell
python -m sapphire messenger run
```
