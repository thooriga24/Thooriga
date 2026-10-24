import {describe,it,expect} from 'vitest';
import {move,toggle,validateFiles,validBrief} from './utils';
const f=(type:string,size=10)=>({type,size} as File);
describe('collection validation',()=>{
 it('accepts supported images',()=>expect(validateFiles([f('image/jpeg'),f('image/webp')],0)).toBe(''));
 it('rejects unsupported files',()=>expect(validateFiles([f('image/gif')],0)).toContain('JPEG'));
 it('limits batch size',()=>expect(validateFiles([f('image/png')],15)).toContain('15'));
 it('limits byte size',()=>expect(validateFiles([f('image/png',16*1024*1024)],0)).toContain('MB'));
 it('requires a useful brief',()=>{expect(validBrief('  ')).toBe(false);expect(validBrief('warm cake')).toBe(true);});
});
describe('human selection',()=>{
 it('selects and restores lower candidates',()=>expect(toggle(['a'],'b')).toEqual(['a','b']));
 it('deselects',()=>expect(toggle(['a','b'],'a')).toEqual(['b']));
 it('reorders without mutation',()=>{const a=['a','b','c'];expect(move(a,1,-1)).toEqual(['b','a','c']);expect(a).toEqual(['a','b','c']);});
 it('keeps bounds',()=>expect(move(['a'],0,-1)).toEqual(['a']));
});

describe('additional upload and shortlist regression cases',()=>{
 it('accepts an empty incoming list',()=>expect(validateFiles([],0)).toBe(''));
 it('accepts exactly the image limit',()=>expect(validateFiles([f('image/png')],14)).toBe(''));
 it('accepts an image exactly at the byte limit',()=>expect(validateFiles([f('image/png',15*1024*1024)],0)).toBe(''));
 it('rejects GIF even when the extension appears usable',()=>expect(validateFiles([f('image/gif')],0)).not.toBe(''));
 it('treats whitespace around short text as insufficient',()=>expect(validBrief('  abc  ')).toBe(false));
 it('keeps input order on no-op move',()=>expect(move(['a','b','c'],2,1)).toEqual(['a','b','c']));
 it('moves a selected item to the right',()=>expect(move(['a','b','c'],0,1)).toEqual(['b','a','c']));
 it('does not modify the original selection when toggling',()=>{const before=['a']; expect(toggle(before,'b')).toEqual(['a','b']);expect(before).toEqual(['a']);});
});
