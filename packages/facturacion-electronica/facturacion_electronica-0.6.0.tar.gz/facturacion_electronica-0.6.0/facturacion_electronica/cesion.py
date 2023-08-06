# -*- coding: utf-8 -*-
from facturacion_electronica.cedente import Cedente as Ced
from facturacion_electronica.cesionario import Cesionario as Ces
from facturacion_electronica.documento import Documento as Doc
from facturacion_electronica.dte import DTE
from facturacion_electronica import clase_util as util
from facturacion_electronica.clase_util import UserError
from lxml import etree
import base64
import collections


class Cesion(DTE):

    def __init__(self, vals):
        util.set_fset_from_keysrom_keys(self, vals)

    @property
    def SecCesion(self):
        if not hasattr(self, '_sec_cesion'):
            return False

    @property
    def Cedente(self):
        if not hasattr(self, '_cedente'):
            return False
        return self._cedente

    @Cedente.setter
    def Cedente(self, vals):
        self._cedente = Ced(vals)

    @property
    def Cesionario(self):
        if not hasattr(self, '_cesionario'):
            return False
        return self._cesionario

    @Cesionario.setter
    def Cesionario(self, vals):
        self._cesionario = Ces(vals)

    @property
    def DeclaracionJurada(self):
        if not hasattr(self, '_declaracion_jurada'):
            return  u'''Se declara bajo juramento que {0}, RUT {1} \
ha puesto a disposicion del cesionario {2}, RUT {3}, el o los documentos donde constan los recibos de las mercaderías entregadas o servicios prestados, \
entregados por parte del deudor de la factura {4}, RUT {5}, de acuerdo a lo establecido en la Ley No. 19.983'''.format(
                self.Emisor.Nombre,
                self.Emisor.Rut,
                self.Cesionario.Nombre,
                self.Cesionario.RUT,
                self.Receptor.Nombre,
                self.Receptor.RUT,
            )
        return self._declaracion_jurada

    @DeclaracionJurada.settter
    def DeclaracionJurada(self, val):
        self._declaracion_jurada = val

    @property
    def ImageAR(self):
        imagen_ar_ids = fields.One2many(
        'account.invoice.imagen_ar',
        'invoice_id',
        string="Imagenes de acuse de recibo",
    )

    @property
    def MontoCesion(self):
        if not hasattr(self, '_monto_cesion'):
            return 0
        return self._monto_cesion

    @MontoCesion.setter
    def MontoCesion(self, val):
        self._monto_cesion = val

    @property
    def xml_dte(self):
        if not hasattr(self, '_xml_dte'):
            return False
        return self._xml_dte

    @xml_dte.setter
    def xml_dte(self, val):
        self._xml_dte = val

    def crear_doc_cedido(self, id):
        xml = '''<DocumentoDTECedido ID="{0}">
{1}
<TmstFirma>{2}</TmstFirma>
</DocumentoDTECedido>
    '''.format(
            id,
            self.sii_xml_dte,
            self.time_stamp(),
        )
        return xml

    def crear_dte_cedido(self, doc):
        xml = '''<DTECedido xmlns="http://www.sii.cl/SiiDte" version="1.0">
{}
</DTECedido>'''.format(doc)
        return xml

    def _crear_info_trans_elec_aec(self, doc, id):
        xml = '''<DocumentoCesion ID="{0}">
{1}
</DocumentoCesion>
'''.format(
            id,
            doc,
        )
        return xml

    def _crear_info_cesion(self, doc):
        xml = '''<Cesion xmlns="http://www.sii.cl/SiiDte" version="1.0">
{1}
</Cesion>
'''.format(
            id,
            doc,
        )
        return xml

    def procesar_recepcion(self, retorno, respuesta_dict ):
        if not 'RECEPCIONAEC' in respuesta_dict:
            return super(CesionDTE, self).procesar_recepcion(retorno, respuesta_dict)
        if respuesta_dict['RECEPCIONAEC']['STATUS'] != '0':
            _logger.warning(connection_status[respuesta_dict['RECEPCIONDTE']['STATUS']])
        else:
            retorno.update({'sii_result': 'Enviado','sii_send_ident':respuesta_dict['RECEPCIONAEC']['TRACKID']})
        return retorno

    def _id_dte(self):
        IdDoc = collections.OrderedDict()
        IdDoc['TipoDTE'] = self.TipoDTE
        IdDoc['RUTEmisor'] = self.Emisor.RUTEmisor
        if not self.partner_id.commercial_partner_id.vat:
            raise UserError("Debe Ingresar RUT Receptor")
        IdDoc['RUTReceptor'] = self.Receptor.RUTRecptor
        IdDoc['Folio'] = self.get_folio()
        IdDoc['FchEmis'] = self.FchEmis
        IdDoc['MntTotal'] = self.currency_id.round(self.amount_total)
        return IdDoc

    def _cedente(self):
        Emisor = collections.OrderedDict()
        Emisor['RUT'] = self.Emisor.RUT
        Emisor['RazonSocial'] = self.Emisor.Nombre
        Emisor['Direccion'] = self.Emisor.Direccion
        Emisor['eMail'] = self.company_id.email or ''
        Emisor['RUTAutorizado'] = collections.OrderedDict()
        Emisor['RUTAutorizado']['RUT'] = self.Cedente.RUT
        Emisor['RUTAutorizado']['Nombre'] = self.Cedente.Nombre
        Emisor['DeclaracionJurada'] = self.DeclaracionJurada
        return Emisor

    def _cesionario(self):
        Receptor = collections.OrderedDict()
        if not self.Cesionario or not self.Cesionario.RUT:
            raise UserError("Debe Ingresar RUT Cesionario")
        Receptor['RUT'] = self.Cesionario.RUT
        Receptor['RazonSocial'] = self.Cesionario.RazonSocial
        Receptor['Direccion'] = self.Cesionario.Direccion
        Receptor['eMail'] = self.Cesionario.eMail
        return Receptor

    def doc_cedido(self):
        id = 'CesDoc1'
        data = collections.OrderedDict()
        data['SeqCesion'] = self.cesion_number
        data['IdDTE'] = self._id_dte()
        data['Cedente'] = self._cedente()
        data['Cesionario'] = self._cesionario()
        data['MontoCesion'] = self._monto_cesion()
        data['UltimoVencimiento'] = self.date_invoice
        data['TmstCesion'] = self.time_stamp()
        xml = dicttoxml.dicttoxml(
            {'item':data}, root=False, attr_type=False).decode() \
            .replace('<item>', '').replace('</item>', '')
        doc_cesion_xml = self._crear_info_trans_elec_aec(xml, id)
        cesion_xml = self._crear_info_cesion(doc_cesion_xml)
        root = etree.XML(cesion_xml)
        xml_formated = etree.tostring(root).decode()
        cesion = self.sign_full_xml(
            xml_formated,
            id,
            'cesion',
        )
        return cesion.replace('<?xml version="1.0" encoding="ISO-8859-1"?>\n','')

    def dte_cedido(self):
        id = "DocCed_" + str(self.sii_document_number)
        xml = self.crear_doc_cedido(id)
        xml_cedido = self.crear_dte_cedido(xml)
        dte_cedido = self.sign_full_xml(
            xml_cedido,
            id,
            'dte_cedido',
        )
        return dte_cedido
