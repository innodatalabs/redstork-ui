import multiprocessing.pool
import trio
from redstork import Document


async def render(pool, pdf_filename, pageno, image_filename, scale=1.0, rect=None):
    '''asynchronously renders PDF page using process pool.'''
    future = pool.apply_async(render_worker, (pdf_filename, pageno, image_filename, scale, rect))
    return await trio.to_thread.run_sync(future.get)

def render_worker(pdf_filename, pageno, image_filename, scale, rect):
    doc = Document(pdf_filename)
    page = doc[pageno]
    page.render(image_filename, scale=scale, rect=rect)
