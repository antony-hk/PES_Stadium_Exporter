import bpy, os, PES_Stadium_Exporter
import datetime
mydate = datetime.datetime.now()

#Create and generate XML contents by object stadium
cl=['\n\t<classes>'
    '\n\t\t<class name="Entity" super="" version="2" />'
    '\n\t\t<class name="Data" super="Entity" version="2" />'
    '\n\t\t<class name="DataSet" super="" version="0" />'
    '\n\t\t<class name="StadiumModel" super="" version="3" />'
	'\n\t\t<class name="EnlightenProbeSet" super="" version="0" />'
    '\n\t\t<class name="EnlightenSystemContainer" super="" version="0" />'
    '\n\t\t<class name="TransformEntity" super="" version="0" />'
    '\n\t\t<class name="ShearTransformEntity" super="" version="0" />'
    '\n\t\t<class name="PivotTransformEntity" super="" version="0" />'
  	'\n\t</classes>'
	'\n\t<entities>'
    '\n\t\t<entity class="DataSet" classVersion="0" addr="0x03172C40" unknown1="296" unknown2="0">'
    '\n\t\t\t<staticProperties>'
    '\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
    '\n\t\t\t\t\t<value hash="0xB8A0BF169F98" />'
    '\n\t\t\t\t</property>'
    '\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
    '\n\t\t\t\t\t<value>0x00000000</value>'
    '\n\t\t\t\t</property>'
  ]
lsRow=['\n\t\t\t</staticProperties>'
      	'\n\t\t\t<dynamicProperties />'
    	'\n\t\t</entity>'
]

foxroot=["\n\t</entities>"
		"\n</fox>"
]

def makeXMLForStadium(filename,dataList, arraySize, assetpath, shearTransformlist, pivotTransformlist, Stadium_Model,TransformEntityList,Stadium_Kinds):
	StadiumModel=str()
	idx1,idx2,idx3=0,0,0
	stid= bpy.context.scene.STID
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="utf-8"?>')
		file.write('\n<fox formatVersion="2" fileVersion="0" originalVersion="{0}">'.format(mydate.strftime("%c")))
		for ls in cl:
			file.write(ls)
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%s">'%arraySize)
		for dtlist in dataList:
			file.write('\n\t\t\t\t\t<value key="{0}">{1}</value>'.format(Stadium_Model[idx1],dtlist))
			idx1+=1
		file.write('\n\t\t\t\t\t<value key="EnlightenProbeSet0000">0x00007200</value>')
		file.write('\n\t\t\t\t\t<value key="EnlightenSystemContainer0000">0x00007500</value>')
		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)
		Enlighten=open(PES_Stadium_Exporter.xml_dir+'EnlightenSystem.xml','rt').read()
		Enlighten=Enlighten.replace("stid",stid)
		file.write(Enlighten)
		for dtlist in dataList:
			StadiumModel=open(PES_Stadium_Exporter.xml_dir+'StadiumModel.xml','rt').read()
			StadiumModel=StadiumModel.replace("DirName",Stadium_Model[idx2])
			StadiumModel=StadiumModel.replace("addrs",dtlist)
			StadiumModel=StadiumModel.replace("owners",dtlist)
			StadiumModel=StadiumModel.replace("assetpath",assetpath[idx2])
			StadiumModel=StadiumModel.replace("ShearTransAddr",shearTransformlist[idx2])
			StadiumModel=StadiumModel.replace("PivotTransAddr",pivotTransformlist[idx2])
			StadiumModel=StadiumModel.replace("TransformEntityListAddr",TransformEntityList[idx2])
			StadiumModel=StadiumModel.replace("kindValue","%s"%Stadium_Kinds[idx2])
			file.write(StadiumModel)
			idx2+=1
		for shearTrans in shearTransformlist:
			shearTransform=open(PES_Stadium_Exporter.xml_dir+'StadiumEntity.xml','rt').read()
			shearTransform=shearTransform.replace("ShearTransAddr",shearTrans)
			shearTransform=shearTransform.replace("PivotTransAddr",pivotTransformlist[idx3])
			file.write(shearTransform)
			idx3+=1
		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

	#Create and generate XML contents by object tv
cltv=[ 
	'\n\t<classes>'
	'\n\t\t<class name="Entity" super="" version="2" />'
    '\n\t\t<class name="Data" super="Entity" version="2" />'
    '\n\t\t<class name="DataSet" super="" version="0" />'
    '\n\t\t<class name="StadiumModel" super="" version="2" />'
    '\n\t\t<class name="TransformEntity" super="" version="0" />'
    '\n\t\t<class name="StadiumTexture" super="" version="1" />'
	'\n\t</classes>'
	'\n\t<entities>'
    '\n\t\t<entity class="DataSet" classVersion="0" addr="0x02D72D90" unknown1="296" unknown2="0">'
    '\n\t\t\t<staticProperties>'
    '\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
    '\n\t\t\t\t\t<value hash="0xB8A0BF169F98" />'
    '\n\t\t\t\t</property>'
    '\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
    '\n\t\t\t\t\t<value>0x00000000</value>'
    '\n\t\t\t\t</property>'
]

tvBox=[ 
		'\n\t\t<entity class="StadiumTexture" classVersion="1" addr="0x02D72EE0" unknown1="168" unknown2="0">'
		'\n\t\t\t<staticProperties>'
		'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>StadiumTexture_box00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>0x02D72D90</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="textureAlias" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>TV_BOX00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="parameterNames" type="String" container="DynamicArray" arraySize="2">'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_1</value>'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_2</value>'
		'\n\t\t\t\t</property>'
 		'\n\t\t\t\t<property name="materialNames" type="String" container="DynamicArray" arraySize="1">'
		'\n\t\t\t\t\t<value>tv_large_c</value>'
		'\n\t\t\t\t</property>'
]

tvLine=[ 
		'\n\t\t<entity class="StadiumTexture" classVersion="1" addr="0xA84B0590" unknown1="168" unknown2="0">'
		'\n\t\t\t<staticProperties>'
		'\n\t\t\t\t<property name="name" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>StadiumTexture_line00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="dataSet" type="EntityHandle" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>0x02D72D90</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="textureAlias" type="String" container="StaticArray" arraySize="1">'
		'\n\t\t\t\t\t<value>TV_LINE00</value>'
		'\n\t\t\t\t</property>'
		'\n\t\t\t\t<property name="parameterNames" type="String" container="DynamicArray" arraySize="2">'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_1</value>'
		'\n\t\t\t\t\t<value>Base_Tex_SRGB_2</value>'
		'\n\t\t\t\t</property>'
 		'\n\t\t\t\t<property name="materialNames" type="String" container="DynamicArray" arraySize="1">'
		'\n\t\t\t\t\t<value>tv_small_c</value>'
		'\n\t\t\t\t</property>'
]
def makeXMLForTv(filename,TvMdl,arraySize,addrs,assetpath,TvBoxSize,TvLineSize):
	idx1,idx2,idx3=0,0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="utf-8"?>')
		file.write('\n<fox formatVersion="2" fileVersion="0" originalVersion="{0}">'.format(mydate.strftime("%c")))

		for ls in cltv:
			file.write(ls)
			
		if "_Large" in str(TvMdl):
			arraySize+=1
		if "_Small" in str(TvMdl):
			arraySize+=1
		file.write('\n\t\t\t\t<property name="dataList" type="EntityPtr" container="StringMap" arraySize="%s">'%arraySize)

		for mdl in TvMdl:
			file.write('\n\t\t\t\t\t<value key="{0}">{1}</value>'.format(mdl,addrs[idx1]))
			idx1+=1
		if "_Large" in str(TvMdl):
			file.write('\n\t\t\t\t\t<value key="StadiumTexture_box00">0x02D72EE0</value>')
		if "_Small" in str(TvMdl):
			file.write('\n\t\t\t\t\t<value key="StadiumTexture_line00">0xA84B0590</value>')

		file.write('\n\t\t\t\t</property>')
		for ls in lsRow:
			file.write(ls)

		for mdl in TvMdl:
			Tv_Mdl=open(PES_Stadium_Exporter.xml_dir+'TvModel.xml','rt').read()
			Tv_Mdl=Tv_Mdl.replace("DirName",mdl)
			Tv_Mdl=Tv_Mdl.replace("addrs",addrs[idx2])
			Tv_Mdl=Tv_Mdl.replace("assetpath",assetpath[idx2])
			file.write(Tv_Mdl)
			idx2+=1
		if "_Large" in str(TvMdl):
			for tvBoxs in tvBox:
				file.write(tvBoxs)
			file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%s">'%TvBoxSize)
		for addr in TvMdl:
			if "_Large" in addr:
				file.write('\n\t\t\t\t\t<value>%s</value>'%addrs[idx3])
				idx3+=1
		if "_Large" in str(TvMdl):
			file.write('\n\t\t\t\t</property>')
			for ls in lsRow:
				file.write(ls)

		if "_Small" in str(TvMdl):
			for tvLines in tvLine:
				file.write(tvLines)
			file.write('\n\t\t\t\t<property name="models" type="EntityPtr" container="DynamicArray" arraySize="%s">'%TvLineSize)

		for addr in TvMdl:
			if "_Small" in addr:
				file.write('\n\t\t\t\t\t<value>%s</value>'%addrs[idx3])
				idx3+=1
		if "_Small" in str(TvMdl):
			file.write('\n\t\t\t\t</property>')
			for ls in lsRow:
				file.write(ls)

		for fr in foxroot:
			file.write(fr)
		file.flush(),file.close()
	return 1

	#Create and generate effect XML contents by object light
Vignetting=['\n\t<setting type="Vignetting" index="0">'
    		'\n\t\t<param id="texturePath" type="path" value="/Assets/pes16/model/bg/common/effect/texture/filter/filter.ftex" />'
    		'\n\t\t<param id="alpha" type="uint" value="0x80" />'
  			'\n\t</setting>'
]
def lightFxXml(filename,sideName,L_Side):
	scn = bpy.context.scene
	idx1,idx2,idx3,idx4,idx5,idx6=0,0,0,0,0,0
	with open(filename, "w", encoding="utf-8") as file:
		file.write('<?xml version="1.0" encoding="UTF-8"?>')
		file.write('\n<effect version="2">')
		if scn.time_mode == "dr" or scn.time_mode == "nr":
			RainDemo=open(PES_Stadium_Exporter.xml_dir+'effect\\RainDemo.xml','rt').read()
			file.write(RainDemo)
		for sd in sideName:
			LightBillboard=open(PES_Stadium_Exporter.xml_dir+'effect\\LightBillboard.xml','rt').read()
			LightBillboard=LightBillboard.replace("iSize","%i"%idx1)
			LightBillboard=LightBillboard.replace("locstar",sd)
			LightBillboard=LightBillboard.replace("stid",scn.STID)
			LT = scn.l_fx_tex
			if LT in ['00','01','04']:
				LR = '30'
			else:
				LR = '45'
			LightBillboard=LightBillboard.replace("%LT",LT)
			LightBillboard=LightBillboard.replace("%LR",LR)
			file.write(LightBillboard)
			idx1+=1
		for LFlare in bpy.data.objects['LensFlare'].children:
			for L_ob in bpy.data.objects[LFlare.name].children:
				lx,ly,lz=L_ob.location.x,L_ob.location.y*-1,L_ob.location.z
				L_ob.rotation_mode = "QUATERNION"
				rw,rx,ry,rz=L_ob.rotation_quaternion.w,L_ob.rotation_quaternion.x*-1,L_ob.rotation_quaternion.y,L_ob.rotation_quaternion.z
				LensFlare=open(PES_Stadium_Exporter.xml_dir+'effect\\LensFlare.xml','rt').read()
				LensFlare=LensFlare.replace("%LSize","%i"%idx2)
				LensFlare=LensFlare.replace("%tx","%f"%lx)
				LensFlare=LensFlare.replace("%ty","%f"%lz)
				LensFlare=LensFlare.replace("%tz","%f"%ly)
				LensFlare=LensFlare.replace("%qx","%f"%rx)
				LensFlare=LensFlare.replace("%qy","%f"%ry)
				LensFlare=LensFlare.replace("%qz","%f"%rz)
				LensFlare=LensFlare.replace("%qw","%f"%rw)
				file.write(LensFlare)
				idx2+=1
		for v in Vignetting:
			file.write(v)
		for Halo in bpy.data.objects['Halo'].children:
			for Halo_ob in bpy.data.objects[Halo.name].children:
				haloSide=str(Halo_ob.parent.name)
				lx,ly,lz=Halo_ob.location.x,Halo_ob.location.y*-1,Halo_ob.location.z
				Halo_ob.rotation_mode = "QUATERNION"
				tex=Halo_ob.HaloTex
				rw,rx,ry,rz=Halo_ob.rotation_quaternion.w,Halo_ob.rotation_quaternion.x,Halo_ob.rotation_quaternion.y*-1,Halo_ob.rotation_quaternion.z
				sx,sy,sz=Halo_ob.scale.x,Halo_ob.scale.y,Halo_ob.scale.z,
				HaloXml=open(PES_Stadium_Exporter.xml_dir+'effect\\Halo.xml','rt').read()
				HaloXml=HaloXml.replace("%hTex","%s"%tex)
				HaloXml=HaloXml.replace("%hSize","%i"%idx5)
				HaloXml=HaloXml.replace("%tx","%f"%lx)
				HaloXml=HaloXml.replace("%ty","%f"%lz)
				HaloXml=HaloXml.replace("%tz","%f"%ly)

				HaloXml=HaloXml.replace("%qx","%f"%rx)
				HaloXml=HaloXml.replace("%qz","%f"%ry)
				HaloXml=HaloXml.replace("%qy","%f"%rz)
				HaloXml=HaloXml.replace("%qw","%f"%rw)

				HaloXml=HaloXml.replace("%Sx","%f"%sx)
				HaloXml=HaloXml.replace("%Sy","%f"%sy)
				HaloXml=HaloXml.replace("%Sz","%f"%sz)
				HaloXml=HaloXml.replace("%R","%u"%Halo_ob.rotY)

				HaloXml=HaloXml.replace("%pvx","0.000000")
				HaloXml=HaloXml.replace("%pvy","0.454784")
				HaloXml=HaloXml.replace("%pvz","0.000000")
				file.write(HaloXml)
				idx5+=1
		if scn.time_mode == "dr" or scn.time_mode == "nr":
			file.write('\n\t<create type="MultiUvScrollScreen" setting="0" />')
			file.write('\n\t<create type="RainDemo" setting="0" />')
		for s in L_Side:
			file.write('\n\t<create type="LightBillboard" setting="%i" floor="upper" dir="%s" />'%(idx3,s))
			idx3+=1
		for LFlare in bpy.data.objects['LensFlare'].children:
			for L_ob in bpy.data.objects[LFlare.name].children:
				file.write('\n\t<create type="LensFlare" setting="%i" />'%idx4)
				idx4+=1
		file.write('\n\t<create type="Vignetting" setting="0" />')
		for Halo in bpy.data.objects['Halo'].children:
			for Halo_ob in bpy.data.objects[Halo.name].children:
				haloSide=str(Halo_ob.parent.name).split('_')[1]
				file.write('\n\t<create type="Halo" setting="%i" floor="upper" dir="%s" />'% (idx6,haloSide.lower()))
				idx6+=1
		file.write('\n</effect>')
		file.flush(),file.close()
	return 1