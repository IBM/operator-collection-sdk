FROM scratch

LABEL name="IBM Operator Collection SDK"
LABEL vendor="IBM"
LABEL summary="The image for the IBM Operator Collection SDK"
LABEL description="This image contains the IBM Operator Collection SDK tool and documentation"

COPY . .


USER 1001