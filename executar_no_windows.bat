@echo off
title Imobiliaria R.M. - Orcamento de Aluguel
python main.py
if errorlevel 1 (
  echo.
  echo Nao foi possivel iniciar. Instale o Python 3 e marque a opcao Add Python to PATH.
  pause
)
