function epvalue = readfrompipeout(obj, epaddr, blksize, bsize, psize)

%READFROMBLOCKPIPEOUT  Read data from a Block PipeOut.
%  epVALUE=READFROMBLOCKPIPEOUT(OBJ,epADDR,BLKSIZE,SIZE) reads SIZE number of elements
%  from a PipeOut endpoint.  The elements of evVALUE are unsigned bytes
%  (8 bits : 0..255) stored as fints (floating point integers).
%  epADDR the endpoint address of the PipeOut endpoint.
%  BLKSIZE is the block size (2..1024).
%
%  epVALUE=READFROMPIPEOUT(OBJ,epADDR,BLKSIZE,SIZE,PSIZE) subdivides the read
%  transfer into smaller packets of size PSIZE.
%  By default, PSIZE = SIZE.
%
%  The valid endpoint address ranges are:
%
%    0x00-0x1F : WireIn
%    0x20-0x3F : WireOut
%    0x40-0x5F : TriggerIn
%    0x60-0x7F : TriggerOut
%    0x80-0x9F : PipeIn
%  * 0xA0-0xBF : PipeOut
%
%  Copyright (c) 2005 Opal Kelly Incorporated
%  $Rev: 210 $ $Date: 2005-10-13 19:54:17 -0700 (Thu, 13 Oct 2005) $

psize = bsize;
%persistent buf pv;
buf(psize,1) = uint8(0);
epvalue(bsize,1) = uint8(0);%!!!
pv = libpointer('uint8Ptr', buf);

calllib('okFrontPanel', 'okFrontPanel_ReadFromBlockPipeOut', obj.ptr, epaddr, blksize, bsize, pv);
%[~, ~, epvalue]=calllib('okFrontPanel', 'okFrontPanel_ReadFromBlockPipeOut', obj.ptr, epaddr, blksize, bsize, pv);
epvalue = get(pv, 'value');
clear buf;
