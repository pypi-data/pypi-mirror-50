# enhanceml 

enhanceml (Enhance Machine Learning model) is a Python library to enhance the prediction of model using various statistical technique. This contains various sub-models which can be fitted over data to predict outcome.

* PBOB (Probability based Best Out of Best outcome): This method is used to enhance the prediction based on probability.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install enhanceml.

```bash
pip install enhanceml
```
   or
```bash
https://github.com/sumitc29/enhanceml.git
```

## Usage

```python
from enhanceml import enhancer

knn=KNeighborsClassifier()
gnb=GaussianNB()

pbob_model=enhancer.PBOB(knn,gnb)

pbob_model.fit(x_train,y_train)
predictions=pbob_model.predict(x_test)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
