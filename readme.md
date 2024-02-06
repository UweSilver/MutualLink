Dynamic Link
```
cmake -B out -DDYNAMIC_LINK=ON
cmake --build out
```

Static Link
```
cmake -B out -DDYNAMIC_LINK=OFF
cmake --build out
```

cmakeのoption指定時は、`-D<オプション名>=ON/OFF`なことに注意