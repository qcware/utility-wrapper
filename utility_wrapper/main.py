from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from openbabel import openbabel

app = FastAPI()

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
