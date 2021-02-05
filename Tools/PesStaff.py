import bpy, os, PES_Stadium_Exporter
import xml.etree.ElementTree as ET
from Tools import PesFoxXML

staff_walk_list = ['gu_england2018A',
				'gu_england2018B',
				'st_flee2018A_non',
				'st_flee2018B_non',
]

result = None
objlist=[]

def importStaffWalk(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	fpkfilename="%sstaff\\#Win\\staff_%s.fpk"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkfilename)
	basedir = os.path.dirname(fpkfilename)
	dirPath ="%s\\addons\\Tools\\Gzs\\xml\\scarecrow\\textures\\"%PES_Stadium_Exporter.AddonsPath
	for root, directories, filenames in os.walk(basedir):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.fmdl':
				if filename in staff_walk_list:
					fmdlPath = os.path.join(root, fileName)
					print('Importing ==> %s' % fileName)
					PES_Stadium_Exporter.importFmdlfile(fmdlPath, "Skeleton_%s" % filename, filename, filename, dirPath, "Staff Walk")
	fpkdfilename="%sstaff\#Win\staff_%s.fpkd"%(exportPath,stid)
	PES_Stadium_Exporter.pack_unpack_Fpk(fpkdfilename)
	basedird = os.path.dirname(fpkdfilename)
	fox2xmlName=str()
	for root, directories, filenames in os.walk(basedird):
		for fileName in filenames:
			filename, extension = os.path.splitext(fileName)
			if extension.lower() == '.fox2':
				if '_walk' in filename:
					fox2xmlName = os.path.join(root, fileName)

	PES_Stadium_Exporter.compileXML(fox2xmlName)
	Staff_Config(self,context,fox2xmlName+'.xml','Staff Walk')

def exportStaffWalk(self, context):
	stid=context.scene.STID
	exportPath=context.scene.export_path
	iarraySize=0
	for ob in bpy.data.objects['Staff Walk'].children:
		if ob.type == "EMPTY":
			iarraySize+=1
	xmlpath='%sstaff\\#Win\\staff_%s_fpkd\\Assets\\pes16\\model\\bg\\%s\\staff\\%s_2018_common_walk.fox2.xml'%(exportPath,stid,stid,stid)
	PesFoxXML.Staff_Walk_xml(xmlpath,iarraySize)
# Select multiple object hierarchy
def SelectableObj(child):
	bpy.ops.object.select_all(action='DESELECT')

	child.select_set(True)
	for ob in bpy.data.objects[child.name].children[:1]:
		ob.select_set(True)
		if ob is not None:
			for ob2 in bpy.data.objects[ob.name].children:
				if ob2 is not None and  ob2.type == "MESH":
					ob2.select_set(True)

# Parsing xml dictionary this script created by themex, full credits for him
def xmlParser(filename):
	modelName_addr_dict = {}
	model_transform_dict = {}

	xmlTree = ET.parse(filename)

	for entities in xmlTree.findall('entities'):
		for entity in entities.findall('entity'):
			if entity.get('class') == 'StadiumModel':
				modelName_addr_dict[entity.get('addr')] = entity
			if entity.get('class') == 'TransformEntity':
				for prop in entity.find('staticProperties').findall('property'):
					if prop.get('name') == 'owner':
						model_addr = prop.find('value').text
						model_transform_dict[modelName_addr_dict[model_addr]] = entity

	return model_transform_dict

def Staff_Config(self,context,fox2xml, cldname):

	# We need get fullname in xml before applied value and duplicate object
	model_transform_dict2 = xmlParser(fox2xml)
	for model in model_transform_dict2.keys():
		fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
		fmdl_name = os.path.splitext(fmdl_name)
		fmdl_name = str(fmdl_name[0]).split('/')[-1]
		objlist.append(fmdl_name)

	# Applied value to each object in xml and duplicate object length in xml
	for ob in bpy.data.objects[cldname].children:
		if ob.type == "EMPTY":
			model_transform_dict = xmlParser(fox2xml)

			for model in model_transform_dict.keys():
				model_name = model.find('staticProperties').findall('property')[0].find('value').text
				fmdl_name = model.find('staticProperties').findall('property')[8].find('value').text
				fmdl_name = os.path.splitext(fmdl_name)
				fmdl_name = str(fmdl_name[0]).split('/')[-1]
				if ob.name == fmdl_name:
					transformEntityPtr = model.find('staticProperties').findall('property')[3].find('value').text
					_direction = model.find('staticProperties').findall('property')[18].find('value').text
					_kind = model.find('staticProperties').findall('property')[19].find('value').text
					_demoGroup = model.find('staticProperties').findall('property')[20].find('value').text
					transform = model_transform_dict[model]

					for property in transform.find('staticProperties').findall('property'):
						addr=property.find('value').text
						if addr is not None:
							ob.scrName = model_name
							ob.scrEntityPtr= addr
							ob.scrTransformEntity = transformEntityPtr
							ob.scrDirection = int(_direction)
							ob.scrKind = int(_kind)
							ob.scrDemoGroup = int(_demoGroup)

						property_val = property.find('value')
						transform_type=property.get('name')	
						if transform_type=='transform_rotation_quat':
							qx,qy,qz,qw= property_val.get('x'), property_val.get('y'), property_val.get('z'), property_val.get('w')
							if (qx,qy,qz,qw) is not None:
								ob.rotation_mode = "QUATERNION"
								ob.rotation_quaternion.w = float(qw)
								ob.rotation_quaternion.x = float(qx)
								ob.rotation_quaternion.y = float(qz)*-1
								ob.rotation_quaternion.z = float(qy)
						if transform_type=='transform_translation':
							tx,ty,tz,tw= property_val.get('x'), property_val.get('y'), property_val.get('z'), property_val.get('w')
							if (tx,ty,tz,tw) is not None:
								ob.location.x = float(tx)
								ob.location.y = float(tz)*-1
								ob.location.z = float(ty)

					# Actually need duplicate object by length-1 of object in xml, but this no (wee fix it in last loop) 
					SelectableObj(ob)
					bpy.ops.object.duplicate()

	del_obj(cldname)

	return 1

def del_obj(cldname):
	
	# In this case we delete last object duplicate, because we no need last object
	for ob in bpy.data.objects[cldname].children:
		if ob.type == "EMPTY":
			if '.' in ob.name:
				_obname = str(ob.name).split('.')[0]
				obLen=objlist.count(_obname)
				if len(str(obLen)) == 1:
					_obLen='.00%s'%obLen
				elif len(str(obLen)) == 2:
					_obLen='.0%s'%obLen
				else:
					_obLen='.%s'%obLen
				if ob.name == _obname+_obLen:
					print('Delete duplicate last object: "%s%s"'%(_obname,_obLen))
					SelectableObj(ob)
					bpy.ops.object.delete()