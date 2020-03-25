#!/bin/bash

# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../../../

GRPC_SERVER_ADDRESS="52.59.227.62"
GRPC_SERVER_PORT=8080
NUM_CLIENTS=100
I_START=0
I_END=49

echo "Starting $NUM_CLIENTS clients."
for ((i = $I_START; i <= $I_END; i++))
do
    echo "Starting client(cid=$i) with partition $i out of $NUM_CLIENTS clients."
    python -m flower_examples.tf_fashion_mnist.client \
      --cid=$i \
      --partition=$i \
      --clients=$NUM_CLIENTS \
      --grpc_server_address=$GRPC_SERVER_ADDRESS \
      --grpc_server_port=$GRPC_SERVER_PORT &
done
echo "Started $NUM_CLIENTS clients."
