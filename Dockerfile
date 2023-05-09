FROM scratch

LABEL name="Operator Collection SDK"
LABEL vendor="IBM"
LABEL summary="The image for the Operator Collection SDK"
LABEL description="This image contains the Operator Collection SDK tool and documentation"

COPY . .


USER 1001