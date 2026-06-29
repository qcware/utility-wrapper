from typing import Optional

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from openbabel import openbabel

app = FastAPI()

@app.get("/healthz", status_code=status.HTTP_204_NO_CONTENT)
def healthz():
    """Liveness/readiness probe target (Promethium /healthz convention)."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/livez", status_code=status.HTTP_200_OK)
def livez():
    """Liveness probe target (Promethium /livez convention)."""
    return Response(status_code=status.HTTP_200_OK)

class OpenBabelConversionRequest(BaseModel):
    input_data: str
    input_format: str
    output_format: str
    use_rigid_option: Optional[bool] = False
    add_hydrogens: Optional[bool] = False

class OpenBabelConversionResponse(BaseModel):
    output_data: str

@app.post("/openbabel/convert", response_model=OpenBabelConversionResponse)
def openbabel_convert(request: OpenBabelConversionRequest):
    conv = openbabel.OBConversion()
    conv.SetInAndOutFormats(request.input_format, request.output_format)
    if request.use_rigid_option:
        conv.SetOptions("r", conv.OUTOPTIONS)

    mol = openbabel.OBMol()
    conv.ReadString(mol, request.input_data)
    if request.add_hydrogens:
        mol.AddHydrogens()

    output_data = conv.WriteString(mol)
    return OpenBabelConversionResponse(
        output_data=output_data
    )
