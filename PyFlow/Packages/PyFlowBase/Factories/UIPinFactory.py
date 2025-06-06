## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.UI.Canvas.UIPinBase import UIPinBase

from PyFlow.Packages.PyFlowBase.UI.UIAnyPin import UIAnyPin
from PyFlow.Packages.PyFlowBase.UI.UIExecPin import UIExecPin


def createUIPin(owningNode, raw_instance):
    if raw_instance.__class__.__name__ == "AnyPin":
        return UIAnyPin(owningNode, raw_instance)
    elif raw_instance.__class__.__name__ == "ExecPin":
        return UIExecPin(owningNode, raw_instance)
    else:
        return UIPinBase(owningNode, raw_instance)
