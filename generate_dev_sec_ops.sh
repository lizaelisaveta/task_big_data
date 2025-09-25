#!/bin/bash
export PYTHONPATH=$(pwd)

set -e

OUTPUT_FILE="dev_sec_ops.yml"

IMAGES=("app" "kafka_consumer")

echo "docker_images:" > $OUTPUT_FILE
for IMAGE in "${IMAGES[@]}"; do
    DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$IMAGE:latest" 2>/dev/null || echo "")
    echo "  - name: $IMAGE" >> $OUTPUT_FILE
    echo "    tag: latest" >> $OUTPUT_FILE
    echo "    digest: \"$DIGEST\"" >> $OUTPUT_FILE
done

MODEL_REPO_DIR="model"
echo "" >> $OUTPUT_FILE
echo "model_commits:" >> $OUTPUT_FILE
pushd $MODEL_REPO_DIR >/dev/null
COMMITS=$(git log -n 5 --pretty=format:"- \"%H\"")
echo "$COMMITS" >> "../$OUTPUT_FILE"
popd >/dev/null

echo "" >> $OUTPUT_FILE
if command -v pytest >/dev/null 2>&1; then
    COVERAGE=$(pytest --cov=src --cov-report=term | grep -Eo '[0-9]{1,3}%' | tail -1 || echo "0%")
else
    COVERAGE="0%"
fi
echo "test_coverage: \"$COVERAGE\"" >> $OUTPUT_FILE

echo "dev_sec_ops.yml generated successfully."
