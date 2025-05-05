{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "private_outputs": true,
      "provenance": [],
      "authorship_tag": "ABX9TyPdvEb7UhQBBlMHyF8Bb7dk",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/ggrighi15/propulsor-intelligence/blob/main/propulsor_juridico.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "ZqmG0rK9Mlwc"
      },
      "outputs": [],
      "source": [
        "C:\\Propulsor\\Propulsor_Juridico.py\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "qZMakaNzNhtn"
      },
      "outputs": [],
      "source": [
        "from fastapi import FastAPI\n",
        "\n",
        "app = FastAPI()\n",
        "\n",
        "@app.get(\"/\")\n",
        "def read_root():\n",
        "    return {\"message\": \"Propulsor Jurídico rodando\"}\n"
      ]
    }
  ]
}